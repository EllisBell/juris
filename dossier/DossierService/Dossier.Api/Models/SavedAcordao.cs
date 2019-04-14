using System.Collections.Generic;

namespace Dossier.Api.Models {
    public class SavedAcordao {
        public string AcordaoId {get; set;}

        public IEnumerable<Comment> Comments {get; set;}
    }
}