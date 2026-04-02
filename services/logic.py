from django.utils import timezone
from datetime import timedelta
from .models import Service, ServiceRecord, Vehicle

def calculate_health_score(vehicle):
    """
    Calculate a health score (0-100) for a vehicle.
    Factors:
    - Mileage: -2 points for every 10k km over 30k (max -20)
    - Service Frequency: -15 points if no service in last 180 days
    - Issues Reported: -10 points for each record with issues in last year
    - Pending Services: -5 points for each pending booking
    """
    score = 100
    now = timezone.now()
    
    # 1. Mileage check
    mileage = vehicle.mileage or 0
    if mileage > 30000:
        over_mileage = (mileage - 30000) // 10000
        score -= min(20, over_mileage * 2)
        
    # 2. Frequency check
    last_service = ServiceRecord.objects.filter(vehicle=vehicle).order_by('-service_date').first()
    if last_service:
        days_since = (now.date() - last_service.service_date).days
        if days_since > 180:
            score -= 15
    else:
        # Never serviced record? Check if vehicle is more than 6 months old
        vehicle_age_days = (now - vehicle.created_at).days
        if vehicle_age_days > 180:
            score -= 15
            
    # 3. Issues reported check (last 365 days)
    one_year_ago = now.date() - timedelta(days=365)
    recent_issues = ServiceRecord.objects.filter(
        vehicle=vehicle, 
        service_date__gte=one_year_ago,
        issues_reported__isnull=False
    ).exclude(issues_reported="").count()
    score -= min(30, recent_issues * 10)
    
    # 4. Pending services check
    pending_bookings = Service.objects.filter(
        customer=vehicle.owner,
        status=Service.STATUS_PENDING
    ).count() # This is a bit loose since Service isn't directly linked to Vehicle yet
    # But it's a good proxy for 'needs attention'
    score -= min(15, pending_bookings * 5)
    
    return max(0, min(100, score))

def get_recommendations(vehicle):
    """
    Generate actionable AI recommendations based on vehicle status and history.
    """
    recommendations = []
    now = timezone.now().date()
    
    # Check for specific service types in history
    records = ServiceRecord.objects.filter(vehicle=vehicle).order_by('-service_date')
    
    # 1. Oil change recommendation
    last_oil = any('oil' in r.work_done.lower() if r.work_done else False for r in records[:5])
    last_oil_date = next((r.service_date for r in records if 'oil' in (r.work_done or '').lower()), None)
    
    if not last_oil_date or (now - last_oil_date).days > 180:
        recommendations.append({
            'type': 'warning',
            'icon': 'fa-oil-can',
            'text': "You should get an oil change soon. Your engine performance may decrease."
        })
        
    # 2. Brake check
    last_brake = next((r.service_date for r in records if 'brake' in (r.work_done or '').lower()), None)
    if not last_brake or (now - last_brake).days > 365:
        recommendations.append({
            'type': 'danger',
            'icon': 'fa-brake-warning',
            'text': "Your brakes haven't been inspected in over a year. Safety check recommended!"
        })
        
    # 3. High mileage
    if (vehicle.mileage or 0) > 80000:
        recommendations.append({
            'type': 'info',
            'icon': 'fa-gauge-high',
            'text': "High mileage detected. A comprehensive suspension and belt check is advised."
        })
        
    # 4. General health
    health_score = calculate_health_score(vehicle)
    if health_score < 60:
        recommendations.append({
            'type': 'primary',
            'icon': 'fa-heart-pulse',
            'text': f"Overall vehicle health is low ({health_score}/100). Consider a Full General Checkup."
        })
        
    return recommendations
