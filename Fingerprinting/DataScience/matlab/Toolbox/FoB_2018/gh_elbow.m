function [e]=gh_elbow(xx,data)

%  program to estimate the three glenohumeral rotations (beta, gamma, beta')
%  from the rotation matrices Rh and Ro of the humerus and forearm w.r.t.
%  the thorax. The orientation of the flexion/extension and pro/supination
%  axis are given w.r.t. the humerus, and are measured at cadaver k4r 
%  (DirkJan Veeger, Mayo clinic, 1994). This program is to be called as
%  function file by levmar.m
%
%  July 21, 1995, Frans van der Helm

beta_a_gh = xx(1);
alfa_el = xx(2);
beta_ps = xx(3);

Rh = data(:,1:3);
Ro = data(:,4:6);
%Ro=Rh'*Ro;

[beta_gh,gamma_gh,dummy]=rotyzy(Rh);

% orientation flexion/extension axis:

el = [0.9916 .0486 -0.1234]'; el=el/norm(el);
% beta_el = asin(-el(3)/sqrt(el(1)^2 + el(3)^2));
% gamma_el = asin(el(2));
% Rel = roty(beta_el)*rotz(gamma_el)
z=cross(el,[0 1 0]');z=z/norm(z);
y=cross(z,el);
Rel=[el y z];

% orientation pro/supination axis (provisionally, needs to be replaced by axis in
% anatomical position):

% ps = [-0.0671 0.9046 0.4212]'; ps=ps/norm(ps);
% ps = [.0283 -.9975 -.0664]'; ps=ps/norm(ps);
%gamma_ps = asin(-ps(1)/sqrt(ps(1)^2 + ps(2)^2));
%alfa_ps = asin(ps(3));
%Rps = rotz(gamma_ps)*rotx(alfa_ps)

% new axis dd. august 7, 1995

ps=[-.1222 .9925 .0129]';ps=ps/norm(ps);

x=cross(ps,[0 0 1]');x=x/norm(x);
z=cross(x,ps);
Rps=[x ps z];

%Ro_dak = roty(beta_gh)*rotz(gamma_gh)*roty(beta_a_gh)*...
%(Rel*rotx(alfa_el)*Rel')*(Rps*roty(beta_ps)*Rps');

Ro_dak = roty(beta_gh)*rotz(gamma_gh)*roty(beta_a_gh)*(Rel*rotx(alfa_el)*Rel')*(Rps*roty(beta_ps)*Rps');

e = diag(Ro_dak'*Ro - eye(3));

