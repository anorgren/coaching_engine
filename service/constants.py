FEW_SHOT_EXAMPLES = [
    # ── Example 1: Boosting Steps ──
    {
        "role": "user",
        "content": """
            Child info:
            - Name: Lily
            - Age: 10
            - Sex: female
            - Preferences: dancing, painting
            - Health conditions: none
            - Height (cm): 140
            - Weight (kg): 40
            
            Child metrics today:
            - Steps: 1500
            - Active minutes: 20
            - Calories in: 2000
            - Sleep hours: 8
            
            Current goals:
            - Complete art sketch (status: on track)
            
            Risk score: 12%
        """
    },
    {
        "role": "assistant",
        "content": """
I suggest we increase Lily’s daily steps to **4,000**—more daily steps will help build her endurance and keep her energized for both painting and dancing.
"""
    },
    {
        "role": "assistant",
        "content": """
Great effort getting 1,500 steps today, Lily! Let’s aim for 4,000 steps tomorrow—maybe try a fun dance break between your painting strokes.
"""
    },

    # ── Example 2: Increasing Active Minutes ──
    {
        "role": "user",
        "content": """
            Child info:
            - Name: Max
            - Age: 14
            - Sex: male
            - Preferences: soccer, video games
            - Health conditions: asthma
            - Height (cm): 160
            - Weight (kg): 55
            
            Child metrics today:
            - Steps: 6000
            - Active minutes: 15
            - Calories in: 2200
            - Sleep hours: 7.5
            
            Current goals:
            - Play soccer twice this week (status: off track)
            
            Risk score: 30%
        """
    },
    {
        "role": "assistant",
        "content": """
            My goal for Max would be to hit **30 minutes of active play**—increasing his active minutes can improve lung capacity and help him better manage his asthma.
            Plus, it’ll get him ready for his next soccer game!
        """
    },
    {
        "role": "assistant",
        "content": """
            Nice work on 6,000 steps, Max! Let’s shoot for at least 30 minutes of active play tomorrow—maybe dribble a soccer ball in the yard or do a quick home workout.
            It’ll help with your asthma and get you ready for your next soccer game!
        """
    },

    # ── Example 3: Prioritizing Sleep ──
    {
        "role": "user",
        "content": """
            Child info:
            - Name: Zoe
            - Age: 13
            - Sex: female
            - Preferences: reading, swimming
            - Health conditions: none
            - Height (cm): 155
            - Weight (kg): 45
            
            Child metrics today:
            - Steps: 8000
            - Active minutes: 45
            - Calories in: 1800
            - Sleep hours: 5.5
            
            Current goals:
            - Read 20 pages per day (status: on track)
            
            Risk score: 20%
        """
    },
    {
        "role": "assistant",
        "content": """
            Let’s aim for **8 hours of sleep** tonight—getting that much rest will improve Zoe’s concentration and recovery, making her reading and swim practice even more enjoyable.
        """
    },
    {
        "role": "assistant",
        "content": """
            Great job with 8,000 steps and 45 active minutes, Zoe! Try winding down with a book instead of screens 30 minutes before bedtime to help reach 8 hours of sleep.
            It’ll help you focus better during your reading and swimming practice.
        """
    },
]
