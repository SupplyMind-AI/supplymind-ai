class RetrainingPolicy:
 def __init__(self,*,min_samples:int,max_psi:float,min_f1:float)->None:self.min_samples=min_samples;self.max_psi=max_psi;self.min_f1=min_f1
 def evaluate(self,snapshot):
  if snapshot.sample_count<self.min_samples:return False,[f'Only {snapshot.sample_count} samples; minimum {self.min_samples}.']
  reasons=[];psi=snapshot.drift_metrics.get('psi');f1=snapshot.metrics.get('f1')
  if psi is not None and float(psi)>=self.max_psi:reasons.append(f'PSI {float(psi):.3f} exceeds {self.max_psi:.3f}.')
  if f1 is not None and float(f1)<self.min_f1:reasons.append(f'F1 {float(f1):.3f} below {self.min_f1:.3f}.')
  return bool(reasons),reasons
