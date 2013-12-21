%module plp
%include typemaps.i


void plp_init();


%typemap(out) char * 
{
	$result = PyString_FromString($1);
}
char * plp_ver();

/*
%typemap(out) int [ANY] 
{       //??
	int i;
	$result = PyList_New($1_dim0);
	for(i = 0; i < $1_dim0; i++){
	    PyObject *o PyInt_FromLong((long) $1[i]);
	    PyList_SetItem($result,i,o);
	}
}
*/

%typemap(out) char * 
{
	$result = PyString_FromString($1);
}
char * plp_rec( const char* inp);


%typemap(out) char * 
{
	$result = PyString_FromString($1);
}
char * plp_bform(int id);


%typemap(out) char * 
{
	$result = PyString_FromString($1);
}
char * plp_forms(int id);


%typemap(out) int * 
{       //??
	$result = PyInt_FromLong(*$1);
}
char * plp_vec(int id, const char * inp);


%typemap(out) char * 
{
	$result = PyString_FromString($1);
}
char * plp_label(int id);

