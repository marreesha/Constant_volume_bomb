/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Copyright (C) YEAR OpenFOAM Foundation
     \\/     M anipulation  |
-------------------------------------------------------------------------------
License
    This file is part of OpenFOAM.

    OpenFOAM is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with OpenFOAM.  If not, see <http://www.gnu.org/licenses/>.

\*---------------------------------------------------------------------------*/

#include "codedFunctionObjectTemplate.H"
#include "fvCFD.H"
#include "unitConversion.H"
#include "addToRunTimeSelectionTable.H"

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

namespace Foam
{

// * * * * * * * * * * * * * * Static Data Members * * * * * * * * * * * * * //

defineTypeNameAndDebug(fullEnthalphyFunctionObject, 0);

addRemovableToRunTimeSelectionTable
(
    functionObject,
    fullEnthalphyFunctionObject,
    dictionary
);


// * * * * * * * * * * * * * * * Global Functions  * * * * * * * * * * * * * //

extern "C"
{
    // dynamicCode:
    // SHA1 = 1c4c2018ebb173e14188cb809e1a55a3b009ee26
    //
    // unique function name that can be checked if the correct library version
    // has been loaded
    void fullEnthalphy_1c4c2018ebb173e14188cb809e1a55a3b009ee26(bool load)
    {
        if (load)
        {
            // code that can be explicitly executed after loading
        }
        else
        {
            // code that can be explicitly executed before unloading
        }
    }
}


// * * * * * * * * * * * * * * * Local Functions * * * * * * * * * * * * * * //

//{{{ begin localCode

//}}} end localCode


// * * * * * * * * * * * * * Private Member Functions  * * * * * * * * * * * //

const fvMesh& fullEnthalphyFunctionObject::mesh() const
{
    return refCast<const fvMesh>(obr_);
}


// * * * * * * * * * * * * * * * * Constructors  * * * * * * * * * * * * * * //

fullEnthalphyFunctionObject::fullEnthalphyFunctionObject
(
    const word& name,
    const Time& runTime,
    const dictionary& dict
)
:
    functionObjects::regionFunctionObject(name, runTime, dict)
{
    read(dict);
}


// * * * * * * * * * * * * * * * * Destructor  * * * * * * * * * * * * * * * //

fullEnthalphyFunctionObject::~fullEnthalphyFunctionObject()
{}


// * * * * * * * * * * * * * * * Member Functions  * * * * * * * * * * * * * //

bool fullEnthalphyFunctionObject::read(const dictionary& dict)
{
    if (false)
    {
        Info<<"read fullEnthalphy sha1: 1c4c2018ebb173e14188cb809e1a55a3b009ee26\n";
    }

//{{{ begin code
    
//}}} end code

    return true;
}


bool fullEnthalphyFunctionObject::execute()
{
    if (false)
    {
        Info<<"execute fullEnthalphy sha1: 1c4c2018ebb173e14188cb809e1a55a3b009ee26\n";
    }

//{{{ begin code
    
//}}} end code

    return true;
}


bool fullEnthalphyFunctionObject::write()
{
    if (false)
    {
        Info<<"write fullEnthalphy sha1: 1c4c2018ebb173e14188cb809e1a55a3b009ee26\n";
    }

//{{{ begin code
    #line 9 "/home/e2/openfoamCases/komarAlph10Sw15/system/controlDict/functions/fullEnthalphy"
// Info << "Writing fullEnthalphy field" << endl;

        if (!mesh().foundObject<volScalarField>("rhoh")) 
        {
            static autoPtr<volScalarField> rhoh;
            rhoh.set
            (
                new volScalarField
                (
                    IOobject
                    (   
                        "rhoh",
                        mesh().time().timeName(),
                        mesh(),
                        IOobject::NO_READ,
                        IOobject::AUTO_WRITE
                    ),
                    mesh(), 
                    dimEnergy/dimVolume
                )
            );
        }
        
        if (!mesh().foundObject<volScalarField>("rhoCH4")) 
        {
            static autoPtr<volScalarField> rhoCH4;
            rhoCH4.set
            (
                new volScalarField
                (
                    IOobject
                    (   
                        "rhoCH4",
                        mesh().time().timeName(),
                        mesh(),
                        IOobject::NO_READ,
                        IOobject::AUTO_WRITE
                    ),
                    mesh(), 
                    dimMass/dimVolume
                )
            );
        }
        
        
        

        if(mesh().time().timeIndex() != 1)
        {
           volScalarField& rhoh = 
                mesh().lookupObjectRef<volScalarField>("rhoh");
            rhoh = 
                mesh().lookupObject<volScalarField>("T") * 
                mesh().lookupObject<volScalarField>("Cv") * 
                mesh().lookupObject<volScalarField>("rho");
                
                
            volScalarField& rhoCH4 = 
                mesh().lookupObjectRef<volScalarField>("rhoCH4");
            rhoCH4 = 
                mesh().lookupObject<volScalarField>("CH4") * 
                mesh().lookupObject<volScalarField>("rho");
                

            if (mesh().time().outputTime())
            {
                rhoh.write();
                rhoCH4.write();
            }
        }
//}}} end code

    return true;
}


bool fullEnthalphyFunctionObject::end()
{
    if (false)
    {
        Info<<"end fullEnthalphy sha1: 1c4c2018ebb173e14188cb809e1a55a3b009ee26\n";
    }

//{{{ begin code
    
//}}} end code

    return true;
}


// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

} // End namespace Foam

// ************************************************************************* //

