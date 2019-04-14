using System.Collections.Generic;

namespace Dossier.Api.Models {
    public class Folder {
        public string Name {get; set;}

        public IEnumerable<int> Acordaos {get; set;}
    }
}