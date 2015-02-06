select sc1.*, sc2.*
from SinaVerified.dbo.status_cls as sc1
inner join SinaVerified.dbo.status_cls as sc2 on sc1.h2_label_id=sc2.h2_label_id and sc1.h1_label_id<>sc2.h1_label_id and sc1.h2_label_id>-1 and sc1.status_id<sc2.status_id

go


select sc1.*, sc2.*
from SinaVerified.dbo.status_cls as sc1
inner join SinaVerified.dbo.status_cls as sc2 on sc1.h3_label_id=sc2.h3_label_id and (sc1.h1_label_id!=sc2.h1_label_id or sc1.h2_label_id!=sc2.h2_label_id)and sc1.h3_label_id>-1
and sc1.status_id<sc2.status_id

go