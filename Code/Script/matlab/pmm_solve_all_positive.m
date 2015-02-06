function pmm_solve_all_positive()
% 

for k=5:7
    [q1,q2,com_list]=pmm_solve_all(k);
    fname=strcat('community_',num2str(k),'_all_positive','.list');
    fid=fopen(fname,'w');
    fprintf(fid, '{"modularity1":%f, "modularity2":%f,"product":%f,"k":%d,"l":0}\n',q1,q2,q1*q2,k);
    for x=1:1:length(com_list)
        fprintf(fid, '%d ',com_list(x));
    end
    fclose(fid);

end
end

function [Q1,Q2,com_list]=pmm_solve_all(k)
% this function aim to compute all eigenvectors of the
% given matrix
% moreover I have to write the result to the file system
load adj_relation
adj_relation=double(adj);
load adj_content
adj_content=double(adj);

% top l eigenvectors
%l=20;
%k=10;

[rows cols]=size(adj_relation);

% compute top l eigenvectors of the modularity matrix
B1=compute_modularity_matrix_easy(adj_relation);
[la_vector1,la_value1]=eig(B1);
%sprintf('finished computing B1 eigenvectors');
B2=compute_modularity_matrix_easy(adj_content);
[la_vector2,la_value2]=eig(B2);
%sprintf('finished computing B2 eigenvectors');

[r1,c1]=find(la_value1>0);
[r2,c2]=find(la_value2>0);

la_vector1=la_vector1(:,c1);
la_vector2=la_vector2(:,c2);

X=[la_vector1, la_vector2];
    
[U_sub,S,V]=svds(X,k-1);

U_norm=U_sub./repmat(sqrt(sum(U_sub.^2,2)),1,size(U_sub,2));

com_list=kmeans(U_norm, k);

Q1=compute_modularity(B1,com_list,adj_relation);
Q2=compute_modularity(B2,com_list,adj_content);

end

function [Q1,Q2,com_list]=pmm_solve_ret(k,l)
% this function aim to compute the largest algerabic eigenvector of the
% given matrix
% moreover I have to write the result to the file system
load adj_relation
adj_relation=double(adj);
load adj_content
adj_content=double(adj);

% top l eigenvectors
%l=20;
%k=10;

[rows cols]=size(adj_relation);

% compute top l eigenvectors of the modularity matrix
B1=compute_modularity_matrix_easy(adj_relation);
[la_vector1,la_value1]=eigs(B1,l,'la');
B2=compute_modularity_matrix_easy(adj_content);
[la_vector2,la_value2]=eigs(B2,l,'la');

[r1,c1]=find(la_value1>0);
[r2,c2]=find(la_value2>0);

% since this situation seldom happens, I just omit it now
if length(c1)<l || length(c2)<l
    sprintf('negative eigenvectors')
    exit(-1)
end

X=[la_vector1, la_vector2];
    
[U,S,V]=svd(X);
U_sub=U(:,[1:k-1]);

U_norm=U_sub./repmat(sqrt(sum(U_sub.^2,2)),1,size(U_sub,2));

com_list=kmeans(U_norm, k);

Q1=compute_modularity(B1,com_list,adj_relation);
Q2=compute_modularity(B2,com_list,adj_content);

end

function Q=compute_modularity(B, com_list,adj)
    H=get_indicator_matrix(adj,com_list);
    [rows cols]=size(H);
    totalQ=0.0;
    for com=1:1:cols
        totalQ=totalQ+H(:,com)'*B*H(:,com);
    end
    Q=totalQ/sum(sum(adj));
end

function com_label=getq()
global q q_head
    % get an element from a queue
    com_label=q(1,q_head);
    q_head=q_head+1;
end

function pushq(com_label)
global q q_tail
    q(1,q_tail)=com_label;
    q_tail=q_tail+1;
end




function mod_matrix=compute_modularity_matrix(adj)
% first compute modularity matrix
edge_count=sum(sum(adj));
[rows cols]=size(adj);
mod_matrix=zeros(rows, cols, 'double');
for r=1:1:rows
    rdegree=sum(adj(r,:));
    for c=r:1:cols
        cdegree=sum(adj(:,c));
        temp=double(adj(r,c))-(rdegree*cdegree/edge_count);
        mod_matrix(r,c)=temp;
        mod_matrix(c,r)=temp;
    end
end
end


function B=compute_modularity_matrix_easy(adj)
% first compute modularity matrix
K=sum(adj);
edge_count=sum(K);
B=double(adj)-(K.'*K)/edge_count;
end

function H = get_indicator_matrix(adj,com)

% Create the indicator matrix from a community list
% giving for each node its community.
%
% Input
%   - adj: symmetrical (binary or weighted) adjacency matrix
%   - com: community list
%
% Output
%   - H: community indicator matrix where H(i,j) is 1 if node i belongs to
%        community j
%
% Author: Erwan Le Martelot
% Date: 06/12/10

    % Number of nodes
    n = length(com);

    % Number of communities
    nc = length(unique(com));

    % Initialise indicator matrix
    H = zeros(n,nc);

    % Fill in matrix
    for i=1:n
        H(i,com(i)) = 1;
    end

end