function pmm_solve_iterative()
% figure out the solution iteratively
load adj_relation
global adj_relation adj_content

adj_relation=double(adj);
load adj_content
adj_content=double(adj);

k=2;
for l=6:2:20
    [q1,q2,com_list]=pmm_solve_iterative_ret(l);
    fname=strcat('community_',num2str(k),'_',num2str(l),'.list');
    fid=fopen(fname,'w');
    fprintf(fid, '{"modularity1":%f, "modularity2":%f,"product":%f,"k":%d,"l":%d}\n',q1,q2,q1*q2,k,l);
    for x=1:1:length(com_list)
        fprintf(fid, '%d ',com_list(x));
    end
    fclose(fid);
end

end

function [Q1,Q2,com_list]=pmm_solve_iterative_ret(l)
% this function aim to implement the pmm algorithm

global adj_relation adj_content

% modularity matrix should be consistent because it is used to decide
% whether the modularity product increased
B1=compute_modularity_matrix_easy(adj_relation);
B2=compute_modularity_matrix_easy(adj_content);

% init the queue and it can not be global here
q=zeros(1,10000);
q_head=1;
q_tail=1;

% next_label going to use
next_label=2;

% first init all the labels 
com_list=ones(1,rows);
[q,q_tail]=pushq(1,q,q_tail);

%compute old modularity product
old_modularity=compute_modularity(B1,com_list,adj_relation)*compute_modularity(B2,com_list,adj_content);

while q_head~=q_tail
    % compute the eigenvector
    [com,q_head]=getq(q,q_head);
    % find the index of the nodes that belong to the given community
    indexes_needed=find(com_list==com);
    
    %sub adj matrix by the indexes
    sub_adj_relation=adj_relation(indexes_needed,indexes_needed);
    sub_adj_content=adj_content(indexes_needed,indexes_needed);
    
    %compute the corresponding modularity matrix
    sub_mod_relation=compute_modularity_matrix_easy(sub_adj_relation);
    sub_mod_content=compute_modularity_matrix_easy(sub_adj_content);
    
    [la_vector1,la_value1]=eigs(sub_mod_relation,l,'la');
    [la_vector2,la_value2]=eigs(sub_mod_content,l,'la');
    
    % find the positive eigenvalue and its corresponding eigenvector
    [r1,c1]=find(la_value1>0);
    [r2,c2]=find(la_value2>0);
    
    la_vector1=la_vector1(:,c1);
    la_vector2=la_vector2(:,c2);
    
    X=[la_vector1, la_vector2];
    
    % I think finding the largest singular vector is enough and no need to
    % normalize it
    [U_sub,S,V]=svds(X,1);
    %U_norm=U_sub./repmat(sqrt(sum(U_sub.^2,2)),1,size(U_sub,2));

    com_list=kmeans(U_sub, 2);
    n_index=find(com_list==2);
    negative_count=length(n_index);
    
    t_membership=com_list;
    % assign new label
    for x=1:1:negative_count
        t_membership(1,indexes_needed(n_index(x)))=next_label;
    end

    new_modularity=compute_modularity(B1,t_membership,adj_relation)*compute_modularity(B2,t_membership,adj_content);
    
    if new_modularity>old_modularity
        old_modularity=new_modularity;
        com_list=t_membership;
        [q,q_tail]=pushq(com,q,q_tail);
        [q,q_tail]=pushq(next_label,q,q_tail);
        next_label=next_label+1;
    end
end

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

function [com_label,q_head]=getq(q,q_head)
%global q q_head
    % get an element from a queue
    com_label=q(1,q_head);
    q_head=q_head+1;
end

function [q,q_tail]=pushq(com_label,q,q_tail)
%global q q_tail
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