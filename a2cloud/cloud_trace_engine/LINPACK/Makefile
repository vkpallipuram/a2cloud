FF = gfortran
FFLAGS = -O3

all: linpackd.exe linpacks.exe linpackd_x87.exe linpacks_x87.exe

linpackd.exe: linpackd.f
	$(FF) $(FFLAGS) -c linpackd.f
	$(FF) $(FFLAGS) linpackd.o -o linpackd.exe

linpacks.exe: linpacks.f
	$(FF) $(FFLAGS) -c linpacks.f
	$(FF) $(FFLAGS) linpacks.o -o linpacks.exe

linpackd_x87.exe: linpacks.f
	$(FF) $(FFLAGS) -mfpmath=387 -c linpackd.f -o linpackd_x87.o
	$(FF) $(FFLAGS) linpackd_x87.o -o linpackd_x87.exe

linpacks_x87.exe: linpacks.f
	$(FF) $(FFLAGS) -mfpmath=387 -c linpacks.f -o linpacks_x87.o
	$(FF) $(FFLAGS) linpacks_x87.o -o linpacks_x87.exe

clean:
	rm -f linpackd.exe linpacks.exe linpackd_x87.exe linpacks_x87.exe *.o

