using System.Collections.Generic;
using Dossier.Core.Entities;
using System.Linq;

namespace Dossier.Api.Models {
    public class SavedAcordaoUpdateDto {
        public int AcordaoId {get; set;}
        public int FolderId {get; set;}

    }
}