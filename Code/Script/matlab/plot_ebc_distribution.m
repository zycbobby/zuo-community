load EBC_53

r=find(EBC_53>0);
bet_distribution=EBC_53(r);

cdfplot(bet_distribution);
