#include <cstdio>
#include <cmath>
#include "molecule.hpp"

void Molecule::print_geom()
{
  for (int i = 0; i < natom; i++)
    printf("%3.0f %8.5f %8.5f %8.5f\n", zvals[i], geom[i][0], geom[i][1], geom[i][2]);
}

void Molecule::print_bonds()
{
  // for (int i = 0; i < natom; i++)
  //   for (int j = i+1; j < natom; j++)
  for (int i = 0; i < natom; i++)
    for (int j = 0; j < i; j++)
      printf("%3d %3d %10.6f\n", i, j, bond(i,j));
}

void Molecule::print_angles()
{
  // for (int i = 0; i < natom; i++)
  //   for (int j = i+1; j < natom; j++)
  //     for (int k = j+1; k < natom; k++)
  for (int i = 0; i < natom; i++)
    for (int j = 0; j < i; j++)
      for (int k = 0; k < j; k++)
	printf("%3d %3d %3d %10.6f\n", i, j, k, angle(i,j,k));
}

void Molecule::print_oop_angles()
{
  // for (int i = 0; i < natom; i++)
  //   for (int j = i+1; j < natom; j++)
  //     for (int k = j+1; k < natom; k++)
  // 	   for (int l = k+1; l < natom; l++)
  // 	     printf("%3d %3d %3d %3d %10.6f\n", i, j, k, l, angle_oop(i,j,k,l));
  for (int i = 0; i < natom; i++)
    for (int k = 0; k < natom; k++)
      for (int j = 0; j < natom; j++)
	for (int l = 0; l < j; l++)
	  if (i!=j && i!=k && i!=l && j!=k && k!=l && bond(i,k) < 4.0 && bond(k,j) < 4.0 && bond(k,l) < 4.0)
	    printf("%3d %3d %3d %3d %10.6f\n", i, j, k, l, angle_oop(i,j,k,l));
}

void Molecule::print_torsion_angles()
{
  
}

void Molecule::rotate(double phi)
{
  
}

void Molecule::translate(double x, double y, double z)
{
  for (int i = 0; i < natom; i++) {
    geom[i][0] += x;
    geom[i][1] += y;
    geom[i][2] += z;
  }
}

// Returns the distance between atoms i and j in bohr.
double Molecule::bond(int i, int j)
{
  return calc_bond(i, j);
}

// Returns the value of the unit vector between atoms i and j
// in the cart direction (cart=0=x, cart=1=y, cart=2=z)
double Molecule::calc_unit(int i, int j, int cart)
{
  return -(geom[i][cart] - geom[j][cart]) / bond(i, j);
}

// Returns the angle between atoms i, j, and k in degrees.
// Atom j is the central atom.
double Molecule::angle(int i, int j, int k)
{
  return calc_angle(i,j,k);
}

//
double Molecule::angle_oop(int i, int j, int k, int l)
{
  return calc_angle_oop(i,j,k,l);
}

//
double Molecule::angle_torsion(int i, int j, int k, int l)
{
  return calc_angle_torsion(i,j,k,l);
}

Molecule::Molecule(int n, int q)
{
  natom = n;
  charge = q;
  zvals = new double[natom];
  geom = new double* [natom];
  for (int i = 0; i < natom; i++) {
    geom[i] = new double[3];
  }
}

Molecule::~Molecule()
{
  delete[] zvals;
  for (int i = 0; i < natom; i++) {
    delete[] geom[i];
  }
  delete[] geom;
}

double Molecule::calc_bond(int i, int j)
{
  double dx = geom[i][0] - geom[j][0];
  double dy = geom[i][1] - geom[j][1];
  double dz = geom[i][2] - geom[j][2];
  return sqrt((dx*dx) + (dy*dy) + (dz*dz));
}

// Calculates the angle between atoms i, j, and k in degrees.
// Atom j is the central atom.
double Molecule::calc_angle(int i, int j, int k)
{
  // return acos((calc_unit(i, j, 0) * calc_unit(j, k, 0)) + 
  // 	      (calc_unit(i, j, 1) * calc_unit(j, k, 1)) + 
  // 	      (calc_unit(i, j, 2) * calc_unit(j, k, 2))) * (180.0/acos(-1.0));
  return acos((calc_unit(j,i,0) * calc_unit(j,k,0)) + 
	      (calc_unit(j,i,1) * calc_unit(j,k,1)) + 
	      (calc_unit(j,i,2) * calc_unit(j,k,2))) * (180.0/acos(-1.0));
}

double Molecule::calc_angle_oop(int i, int j, int k, int l)
{
  // \mathrm{sin } \theta_{ijkl} = \frac{\mathbf{\tilde{e}_{kj}} \times \mathbf{\tilde{e}_{kl}}}{\mathrm{sin } \phi_{jkl}} \cdot \mathbf{\tilde{e}_{ki}}

  // double ekj[3] = {calc_unit(k, j, 0), calc_unit(k, j, 1), calc_unit(k, j, 2)};
  // double ekl[3] = {calc_unit(k, l, 0), calc_unit(k, l, 1), calc_unit(k, l, 2)};
  // double eki[3] = {calc_unit(k, i, 0), calc_unit(k, i, 1), calc_unit(k, i, 2)};

  // double ekj_cross_kl[3];
  // ekj_cross_kl[0] = (ekj[1]*ekl[2]) - (ekj[2]*ekl[1]);
  // ekj_cross_kl[1] = (ekj[2]*ekl[0]) - (ekj[0]*ekl[2]);
  // ekj_cross_kl[2] = (ekj[0]*ekl[1]) - (ekj[1]*ekl[0]);

  // double ekj_cross_kl_dot_ki[3];
  // ekj_cross_kl_dot_ki[0] = ekj_cross_kl[0] * eki[0];
  // ekj_cross_kl_dot_ki[1] = ekj_cross_kl[1] * eki[1];
  // ekj_cross_kl_dot_ki[2] = ekj_cross_kl[2] * eki[2];

  // double theta = (ekj_cross_kl_dot_ki[0] + ekj_cross_kl_dot_ki[1] + ekj_cross_kl_dot_ki[2])/sin(angle(j,k,l));

  // if (theta < -1.0) theta = asin(-1.0);
  // else if (theta > 1.0) theta = asin(1.0);
  // else theta = asin(theta);

  double ejkl_x = (calc_unit(k,j,1) * calc_unit(k,l,2)) - (calc_unit(k,j,2) * calc_unit(k,l,1));
  double ejkl_y = (calc_unit(k,j,2) * calc_unit(k,l,0)) - (calc_unit(k,j,0) * calc_unit(k,l,2));
  double ejkl_z = (calc_unit(k,j,0) * calc_unit(k,l,1)) - (calc_unit(k,j,1) * calc_unit(k,l,0));
  
  double exx = ejkl_x * calc_unit(k,i,0);
  double eyy = ejkl_y * calc_unit(k,i,1);
  double ezz = ejkl_z * calc_unit(k,i,2);

  double theta = (exx + eyy + ezz)/sin(angle(j,k,l));

  if (theta < -1.0) theta = asin(-1.0);
  else if (theta > 1.0) theta = asin(1.0);
  else theta = asin(theta);

  return theta * (180.0/acos(-1.0));
}

double Molecule::calc_angle_torsion(int i, int j, int k, int l)
{
  return 0.0;
}

void Molecule::calc_bonds()
{

}

void Molecule::calc_angles()
{
  // // calculate the unit vector between each atom
  // for (int i = 0; i < natom; i++) {
  //   ex[i][i] = ey[i][i] = ez[i][i] = 0.0;
  //   for (int j = i+1; j < natom; j++) {
  //     ex[i][j] = ex[j][i] = -(geom[i][0] - geom[j][0]) / get_bond(i, j);
  //     ey[i][j] = ey[j][i] = -(geom[i][1] - geom[j][1]) / get_bond(i, j);
  //     ez[i][j] = ez[j][i] = -(geom[i][2] - geom[j][2]) / get_bond(i, j);
  //   }
  // }

  // // calculate the dot product between two unit vectors spanning three atoms,
  // // then take the arccosine
  // for (int i = 0; i < natom; i++)
  //   for (int j = i+1; j < natom; i++)
  //     for (int k = j+1; k < natom; k++)
  // 	double eij = (ex[i][j]);
}

void Molecule::calc_oop_angles()
{

}

void Molecule::calc_torsion_angles()
{

}
