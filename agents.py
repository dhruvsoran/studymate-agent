from datetime import date, timedelta, datetime, time

def time_add_minutes(t: time, minutes: int):
    dt = datetime.combine(date.today(), t) + timedelta(minutes=minutes)
    return dt.time()

class StudyPlannerAgent:
    def __init__(self, memory_conn=None):
        self.memory_conn = memory_conn

    def _generate_daily_blocks(self, day_date, available_hours, preferred_start=None):
        blocks_count = int((available_hours * 60) // 30)
        blocks = []

        if preferred_start:
            try:
                start = datetime.strptime(preferred_start.split("-")[0], "%H:%M").time()
            except:
                start = time(18, 0)
        else:
            start = time(18, 0)

        t = start
        for _ in range(blocks_count):
            blocks.append(t.strftime("%H:%M"))
            t = time_add_minutes(t, 30)
        return blocks

    def plan(self, user_id, goal, deadline_str, hours_per_day, topics, preferred_times=None):
        today = date.today()
        deadline = date.fromisoformat(deadline_str)
        days = [(today + timedelta(days=i)).isoformat()
                for i in range((deadline - today).days + 1)]

        schedule = []
        ti = 0

        for d in days:
            blocks = self._generate_daily_blocks(d, hours_per_day, preferred_times)
            for start in blocks:
                topic = topics[ti % len(topics)]
                schedule.append({
                    "date": d,
                    "start": start,
                    "duration_minutes": 25,
                    "topic": topic
                })
                ti += 1

        return schedule

def simulate_miss_and_replan(user_id, plan, miss_index=0):
    plan2 = [dict(b) for b in plan]
    missed = plan2.pop(miss_index)
    missed["date"] = plan2[-1]["date"]
    plan2.append(missed)
    return plan2
