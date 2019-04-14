using System;
using System.Collections.Generic;

namespace Dossier.Core.Entities
{
    public class Folder : IEntity
    {
        public int Id {get; set;}
        public string Name {get; set;}
        public IEnumerable<SavedAcordao> SavedAcordaos {get; set;}
    }
}
