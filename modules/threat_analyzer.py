import re
PATTERNS=[
 (re.compile(r"\b(urgent|immediately|act now|within 24 hours|account suspended)\b",re.I),20,"Urgency or pressure language"),
 (re.compile(r"\b(otp|one[- ]time password|password|pin|cvv|bank details)\b",re.I),25,"Requests for credentials or financial details"),
 (re.compile(r"\b(prize|lottery|winner|claim your reward|free gift)\b",re.I),15,"Prize or reward bait"),
 (re.compile(r"\b(verify your account|confirm your identity|KYC update)\b",re.I),15,"Account verification request"),
 (re.compile(r"\b(send money|payment failed|refund|transfer funds)\b",re.I),15,"Money or payment request"),
]
def analyze_message(message:str)->dict:
 score=0; signals=[]
 if re.search(r"(https?://\S+|www\.\S+)",message,re.I): score+=20; signals.append("Contains a URL or web address")
 for pattern,weight,label in PATTERNS:
  if pattern.search(message): score+=weight; signals.append(label)
 score=min(score,100)
 label="High warning signs" if score>=60 else "Some warning signs" if score>=30 else "Few configured warning signs"
 return {"score":score,"signals":signals,"label":label}
