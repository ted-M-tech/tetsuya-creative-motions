// Shared practice-score palette; missing observations are neutral, never zero.
export const scoreColor=score=>typeof score!=='number'||!Number.isFinite(score)?'#69717b':score>=90?'#248044':score>=75?'#0071e3':score>=50?'#b76500':'#b3261e';
