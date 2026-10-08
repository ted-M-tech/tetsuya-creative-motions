// Proposed LP offer only. Not a checkout catalogue: paid sales remain disabled.
// Existing contracts and server billing prices are deliberately independent.
export const LAUNCH_OFFER=Object.freeze({monthly:1480,firstMonth:980,annual:11760,lifetimeEstimate:59800,trialDays:7});
export const annualComparison=Object.freeze({regularTotal:LAUNCH_OFFER.monthly*12,saving:LAUNCH_OFFER.monthly*12-LAUNCH_OFFER.annual,percent:((1-LAUNCH_OFFER.annual/(LAUNCH_OFFER.monthly*12))*100).toFixed(1)});
