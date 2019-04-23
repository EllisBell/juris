using System.Collections.Generic;
using Dossier.Core.Entities;
using System.Linq;

namespace Dossier.Api.Models {
    public class SavedAcordaoDto {
        public int Id {get; set;}
        
        public int AcordaoId {get; set;}

        public IEnumerable<CommentDto> Comments {get; set;}

        public static SavedAcordaoDto FromEntity(SavedAcordao sa) => new SavedAcordaoDto()
        {
            Id = sa.Id,
            AcordaoId = sa.OriginalAcordaoId,
            Comments = sa.Comments.Select(c => CommentDto.FromEntity(c))
        };
    }
}