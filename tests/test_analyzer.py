from modules.threat_analyzer import analyze_message
def test_suspicious_scores_higher():
 assert analyze_message("URGENT verify your account at https://example.invalid and send OTP")["score"] > analyze_message("See you at 5 pm")["score"]
def test_score_bounded():
 assert 0 <= analyze_message("urgent OTP password pin CVV lottery https://x.invalid")["score"] <= 100
