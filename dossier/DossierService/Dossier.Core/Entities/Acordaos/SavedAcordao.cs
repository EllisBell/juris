using System.Collections.Generic;

namespace Dossier.Core.Entities 
{
    public class SavedAcordao : IEntity
     {
        public int Id {get; set;}
        public int OriginalAcordaoId {get; set;}
        public Folder Folder {get; set;}
        public IEnumerable<Comment> Comments {get; set;}
    }
}