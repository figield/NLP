%module plp
%include typemaps.i


void plp_init();


%typemap(out) char * 
{
	$result = PyString_FromString($1);
}
char * plp_ver();


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
{   
	$result = PyInt_FromLong(*$1);
}
char * plp_vec(int id, const char * inp);


%typemap(out) char * 
{
	$result = PyString_FromString($1);
}
char * plp_label(int id);

