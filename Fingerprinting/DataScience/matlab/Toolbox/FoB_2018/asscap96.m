function S = asscap96(ac,ts,ai)

xs = (ac-ts) / norm(ac-ts);
zhulp = cross(xs,(ac-ai));
zhulp = zhulp/norm(zhulp);
ys = cross(zhulp,xs);
zs = cross(xs,ys);

S=[xs,ys,zs];

