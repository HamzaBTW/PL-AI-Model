import random

def get_commentary_template(outcome, club, opponent, venue, probability):
    venue_str = "at home" if venue == "Home" else "on the road"
    top_prob = probability * 100
    win_templates = [
        f"And it's looking good for {{club}} {{venue_str}}! Our model gives them a {{top_prob:.1f}}% chance to win against {{opponent}}.",
        f"{{club}} fans will be delighted! There's a strong {{top_prob:.1f}}% probability of victory over {{opponent}} {{venue_str}}.",
        f"The odds are in favor of {{club}} {{venue_str}}, with a {{top_prob:.1f}}% chance to secure all three points against {{opponent}}.",
        f"{{club}} are tipped to triumph {{venue_str}} versus {{opponent}}, boasting a {{top_prob:.1f}}% win probability."
    ]
    draw_templates = [
        f"It's going to be a tight match between {{club}} and {{opponent}} {{venue_str}}. The most likely outcome is a draw, with a {{top_prob:.1f}}% probability.",
        f"Neither side is expected to dominate as {{club}} faces {{opponent}} {{venue_str}}. A draw is the most probable result at {{top_prob:.1f}}%.",
        f"Expect a balanced contest! {{club}} and {{opponent}} {{venue_str}} are predicted to share the spoils, with a {{top_prob:.1f}}% chance of a draw.",
        f"The stats suggest a stalemate: {{club}} vs {{opponent}} {{venue_str}} has a {{top_prob:.1f}}% likelihood of ending level."
    ]
    lose_templates = [
        f"Tough times ahead for {{club}} {{venue_str}} as they face {{opponent}}. The model predicts a {{top_prob:.1f}}% chance of defeat.",
        f"{{club}} might struggle {{venue_str}} against {{opponent}}, with a {{top_prob:.1f}}% probability of losing this one.",
        f"The forecast isn't bright for {{club}} {{venue_str}}: {{top_prob:.1f}}% chance of a loss to {{opponent}}.",
        f"{{opponent}} are favored to come out on top as {{club}} play {{venue_str}}, with a {{top_prob:.1f}}% chance of defeat for the home side."
    ]
    uncertain_templates = [
        f"The match between {{club}} and {{opponent}} {{venue_str}} is hard to call. Stay tuned for surprises!",
        f"It's anyone's game as {{club}} take on {{opponent}} {{venue_str}}. The model can't pick a clear favorite.",
        f"Unpredictable! {{club}} vs {{opponent}} {{venue_str}} could go either way.",
        f"No clear winner in sight for {{club}} and {{opponent}} {{venue_str}}. Football fans, expect the unexpected!"
    ]
    templates = {
        'win': win_templates,
        'draw': draw_templates,
        'lose': lose_templates,
        'uncertain': uncertain_templates
    }
    chosen_templates = templates.get(outcome.lower(), uncertain_templates)
    template = random.choice(chosen_templates)
    return template.format(club=club, opponent=opponent, venue_str=venue_str, top_prob=top_prob) 