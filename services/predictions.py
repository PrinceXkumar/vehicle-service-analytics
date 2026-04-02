"""
ML Predictions module for the AutoInsight system.
Uses rule-based analysis of historical service data to predict:
  - Next service date (based on average interval between services)
  - Estimated service cost (based on service type averages)
"""

from django.utils import timezone
from datetime import timedelta
from collections import defaultdict


class ServicePredictor:
    """Predicts next service date and estimated cost from historical data."""

    # Default service cost estimates (in ₹) when no historical data exists
    DEFAULT_COSTS = {
        'oil_change': {'min': 1500, 'max': 3000, 'avg': 2250},
        'tyre_replacement': {'min': 3000, 'max': 8000, 'avg': 5500},
        'brake_inspection': {'min': 1000, 'max': 4000, 'avg': 2500},
        'general_checkup': {'min': 500, 'max': 2000, 'avg': 1250},
    }

    # Default interval in days between services
    DEFAULT_INTERVAL_DAYS = 90  # 3 months

    @classmethod
    def predict_next_service_date(cls, user):
        """
        Predict when the user's next service should be scheduled.
        Uses the average interval between past services.
        Returns a dict with prediction details.
        """
        from .models import Service

        services = Service.objects.filter(
            customer=user
        ).order_by('created_at')

        if services.count() < 1:
            return {
                'date': (timezone.now() + timedelta(days=cls.DEFAULT_INTERVAL_DAYS)).date(),
                'days_from_now': cls.DEFAULT_INTERVAL_DAYS,
                'confidence': 'Low',
                'method': 'Default (no history)',
                'data_points': 0,
            }

        if services.count() == 1:
            last_service = services.last()
            predicted_date = last_service.created_at + timedelta(days=cls.DEFAULT_INTERVAL_DAYS)
            days_from_now = (predicted_date - timezone.now()).days
            return {
                'date': predicted_date.date(),
                'days_from_now': max(days_from_now, 0),
                'confidence': 'Low',
                'method': 'Default interval (1 data point)',
                'data_points': 1,
            }

        # Calculate average interval between services
        dates = list(services.values_list('created_at', flat=True))
        intervals = []
        for i in range(1, len(dates)):
            delta = (dates[i] - dates[i - 1]).days
            if delta > 0:
                intervals.append(delta)

        if not intervals:
            avg_interval = cls.DEFAULT_INTERVAL_DAYS
            confidence = 'Low'
        elif len(intervals) < 3:
            avg_interval = sum(intervals) / len(intervals)
            confidence = 'Medium'
        else:
            avg_interval = sum(intervals) / len(intervals)
            confidence = 'High'

        last_service = services.last()
        predicted_date = last_service.created_at + timedelta(days=int(avg_interval))
        days_from_now = (predicted_date - timezone.now()).days

        return {
            'date': predicted_date.date(),
            'days_from_now': max(days_from_now, 0),
            'confidence': confidence,
            'method': f'Average of {len(intervals)} intervals (~{int(avg_interval)} days)',
            'data_points': len(dates),
        }

    @classmethod
    def predict_service_cost(cls, user=None, service_type=None):
        """
        Predict estimated service cost.
        Uses ServiceRecord costs if available, otherwise uses defaults.
        Returns a dict with cost range and confidence.
        """
        from .models import ServiceRecord

        # Try to get historical cost data from ServiceRecord
        records = ServiceRecord.objects.all()
        if records.exists():
            costs = list(records.values_list('parts_cost', 'labor_cost'))
            total_costs = [(float(p) + float(l)) for p, l in costs if (float(p) + float(l)) > 0]

            if total_costs:
                avg_cost = sum(total_costs) / len(total_costs)
                min_cost = min(total_costs)
                max_cost = max(total_costs)

                return {
                    'min': int(min_cost),
                    'max': int(max_cost),
                    'avg': int(avg_cost),
                    'display': f'₹{int(min_cost):,} – ₹{int(max_cost):,}',
                    'confidence': 'High' if len(total_costs) >= 5 else 'Medium',
                    'data_points': len(total_costs),
                }

        # Fallback to default costs based on service type
        if service_type and service_type in cls.DEFAULT_COSTS:
            cost_data = cls.DEFAULT_COSTS[service_type]
        else:
            # Average across all types
            all_avgs = [v['avg'] for v in cls.DEFAULT_COSTS.values()]
            all_mins = [v['min'] for v in cls.DEFAULT_COSTS.values()]
            all_maxs = [v['max'] for v in cls.DEFAULT_COSTS.values()]
            cost_data = {
                'min': int(sum(all_mins) / len(all_mins)),
                'max': int(sum(all_maxs) / len(all_maxs)),
                'avg': int(sum(all_avgs) / len(all_avgs)),
            }

        return {
            'min': cost_data['min'],
            'max': cost_data['max'],
            'avg': cost_data['avg'],
            'display': f'₹{cost_data["min"]:,} – ₹{cost_data["max"]:,}',
            'confidence': 'Low',
            'data_points': 0,
        }

    @classmethod
    def get_customer_predictions(cls, user):
        """
        Get all predictions for a customer in a single call.
        Returns a formatted dict ready for template rendering.
        """
        date_prediction = cls.predict_next_service_date(user)
        cost_prediction = cls.predict_service_cost(user=user)

        # Format the next service date nicely
        days = date_prediction['days_from_now']
        if days == 0:
            date_display = 'Service overdue!'
        elif days <= 7:
            date_display = f'In {days} days'
        elif days <= 30:
            weeks = days // 7
            date_display = f'In ~{weeks} week{"s" if weeks > 1 else ""}'
        else:
            date_display = date_prediction['date'].strftime('%b %d, %Y')

        return {
            'next_service_date': date_display,
            'next_service_exact': date_prediction['date'].strftime('%B %d, %Y'),
            'days_until_service': days,
            'estimated_cost': cost_prediction['display'],
            'cost_avg': f'₹{cost_prediction["avg"]:,}',
            'confidence': date_prediction['confidence'],
            'cost_confidence': cost_prediction['confidence'],
            'data_points': date_prediction['data_points'],
            'method': date_prediction['method'],
        }
