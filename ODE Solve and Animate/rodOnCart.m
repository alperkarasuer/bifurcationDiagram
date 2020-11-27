close
clear
clc

syms x(t) L theta(t) m1 m2 g F1 F2 F I

animFps = 30;
animRange = [0 20];
initCond = [3*pi/4 0 0 0]; % Initial Conditions

% Positions
xRod = x + L*sin(theta);
yRod = -L*cos(theta);
xCart = x;
yCart = 0;

% Speeds
vxRod = diff(xRod);
vyRod = diff(yRod);
vxCart = diff(xCart);
vyCart = diff(yCart);

% Accelerations
axRod = diff(xRod,2);
ayRod = diff(yRod,2);
axCart = diff(xCart,2);
ayCart = diff(yCart,2);

% Equations of motion
eqx_1 = F2 == m1*axRod;
eqy_1 = F1 - m1*g == m1*ayRod;
eqx_2 = F - F2 == m2*axCart;
torque = I*diff(theta,2) == -F1*L*sin(theta) - F2*L*cos(theta);

% Solve for internal forces
internalForces = solve([eqx_1 eqy_1],[F1 F2]);


% Substitute internal forces
eqnRed_1 = subs(eqx_2,[F1 F2],[internalForces.F1, internalForces.F2]);
eqnRed_2 = subs(torque,[F1 F2],[internalForces.F1, internalForces.F2]);

% Variables (mass, mom. of Inertia etc)
m2 = 0.5;
m1 = 0.2;
L = 0.3;
I = 0.006;
g = 9.8;
F = 0; % Force applied on cart

eqn_1 = subs(eqnRed_1);
eqn_2 = subs(eqnRed_2);

[V,S] = odeToVectorField(eqn_1,eqn_2); % Convert to first order sys

f = matlabFunction(V,'vars',{'t','Y'}); 

sols = ode45(f,animRange, initCond); % Solve ODE


% Positions as function of time - for animation.
x_1 = @(t) deval(sols,t,3) + L*sin(deval(sols,t,1));
y_1 = @(t) -L*cos(deval(sols,t,1));
x_2 = @(t) deval(sols,t,3);
y_2 = @(t) 0;

% Rod CoM
figure()
ax = gca;
fanimator(@(t) plot(x_1(t),y_1(t),'ro','MarkerSize',4,'MarkerFaceColor','r'),'FrameRate',animFps,'AnimationRange',animRange);
axis equal;

hold on;
% Cart CoM
fanimator(@(t) plot(x_2(t),y_2(t),'go','MarkerSize',7.5,'MarkerFaceColor','g'),'FrameRate',animFps,'AnimationRange',animRange);
% Connect two particles
fanimator(@(t) plot([x_1(t) x_2(t)],[y_1(t) y_2(t)],'g-'),'FrameRate',animFps,'AnimationRange',animRange);

% Timer
fanimator(@(t) text(0.75,0.75,"Timer: "+num2str(t,2)),'FrameRate',animFps,'AnimationRange',animRange);
line(ax.XLim, [0 0],'LineStyle','-','Color','#0072BD');
ylabel('Y Axis (m)');
xlabel('X Axis (m)');
title('Inverted Pendulum On Cart');
hold off;

playAnimation
