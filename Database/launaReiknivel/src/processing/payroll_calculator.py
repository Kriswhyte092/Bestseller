from datetime import datetime, timedelta


class payroll_calculator:
    def calculate_payroll(self, users, shifts):
        payroll_data = []
        for employee in users:
            
            employee_shifts = [shift for shift in shifts if shift['user_id'] == employee['id']]
            
            DV = 0
            EV = 0
            NV = 0
            YV = 0
            total_worked_hours = 0.0
            
            for shift in employee_shifts:
                total_worked_hours += self.calculate_worked_hours(shift)
                D, E, N = self.calculate_hours(shift) 
                DV += D
                EV += E
                NV += N
            
            if total_worked_hours == 0:
                continue
            

            payroll_data.append({
                'employee_name': employee['legal_name']+ ' ' + employee['lastname'],
                'worked_hours': total_worked_hours,
                'DV': DV,
                'EV': EV,
                'NV': NV,
                'YV': YV,
            })
        
        return payroll_data

    def calculate_worked_hours(self, shift):
        clock_in = datetime.strptime(shift['clock_in'], '%Y-%m-%dT%H:%M:%S%z')
        clock_out = datetime.strptime(shift['clock_out'], '%Y-%m-%dT%H:%M:%S%z')

        worked_hours = (clock_out - clock_in).seconds / 3600
        #if shift['break_minutes'] > 0:
        #    worked_hours -= shift['break_minutes']
        
        return round(worked_hours, 2)

    def calculate_hours(self, shift):
        clock_in = datetime.strptime(shift['clock_in'], '%Y-%m-%dT%H:%M:%S%z')
        clock_out = datetime.strptime(shift['clock_out'], '%Y-%m-%dT%H:%M:%S%z')
        date = shift['scheduled_start'].split(":")[0].split("T")[0]
        if self.is_weekend(date):
            return self.calculate_weekend_hours(clock_in, clock_out)

        regular_hours = timedelta(0)
        after_hours = timedelta(0)
        nighttime_hours = timedelta(0)

        # Time thresholds
        day_start = clock_in.replace(hour=7, minute=0, second=0, microsecond=0)
        evening_start = clock_in.replace(hour=18, minute=0, second=0, microsecond=0)
        midnight_start = clock_in.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        next_day_start = clock_in.replace(hour=7, minute=0, second=0, microsecond=0) + timedelta(days=1)

        while clock_in < clock_out:
            if day_start <= clock_in < evening_start:
                end_time = min(clock_out, evening_start)
                regular_hours += end_time - clock_in
                clock_in = end_time
            elif evening_start <= clock_in < midnight_start:
                end_time = min(clock_out, midnight_start)
                after_hours += end_time - clock_in
                clock_in = end_time
            elif midnight_start <= clock_in < next_day_start:
                end_time = min(clock_out, next_day_start)
                nighttime_hours += end_time - clock_in
                clock_in = end_time
            else:
                break

        regular_hours_total = regular_hours.total_seconds() / 3600
        after_hours_total = after_hours.total_seconds() / 3600
        nighttime_hours_total = nighttime_hours.total_seconds() / 3600

        return round(regular_hours_total, 2), round(after_hours_total, 2), round(nighttime_hours_total, 2) 

    def calculate_weekend_hours(self, clock_in, clock_out):
        regular_hours = timedelta(0)
        nighttime_hours = timedelta(0)

        # Time thresholds
        day_start = clock_in.replace(hour=7, minute=0, second=0, microsecond=0)
        midnight_start = clock_in.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        next_day_start = clock_in.replace(hour=7, minute=0, second=0, microsecond=0) + timedelta(days=1)

        while clock_in < clock_out:
            if day_start <= clock_in < midnight_start:
                end_time = min(clock_out, midnight_start)
                regular_hours += end_time - clock_in
                clock_in = end_time
            elif midnight_start <= clock_in < next_day_start:
                end_time = min(clock_out, next_day_start)
                nighttime_hours += end_time - clock_in
                clock_in = end_time
            else:
                break

        regular_hours_total = regular_hours.total_seconds() / 3600
        nighttime_hours_total = nighttime_hours.total_seconds() / 3600

        return 0.0, round(regular_hours_total, 2), round(nighttime_hours_total, 2)

    def is_weekend(self, date):
        date = datetime.strptime(date, '%Y-%m-%d')
        return date.weekday() >= 5

## bæta við is_red_day(): 

#p = PayrollCalculator()
#user = [{
#    'id': 21451107
#}]
#shift = [{
#'shift_id': '3657205863:2024-12-20', 
#'user_id': 21451107, 
#'scheduled_start': '2024-12-20T08:00:00+00:00', 
#'scheduled_end': '2024-12-20T14:40:00+00:00', 
#'clock_in': '2024-12-20T08:00:00+00:00', 
#'clock_out': '2024-12-21T04:40:00+00:00', 
#'break_minutes': 0, 
#'status': 'approved', 
#'location_id': 16772428, 
#'position_id': 16944354
#}]
#print(p.calculate_payroll(user, shift))

