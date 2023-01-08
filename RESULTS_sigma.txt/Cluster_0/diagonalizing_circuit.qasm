OPENQASM 2.0;
include "qelib1.inc";
qreg q[4];
h q[2];
cx q[2],q[0];
h q[2];
cx q[3],q[1];
h q[3];
