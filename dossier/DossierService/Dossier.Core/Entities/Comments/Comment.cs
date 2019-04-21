using System;

namespace Dossier.Core.Entities 
{
    public class Comment : IEntity 
    {
        public int Id {get;set;}
        public string Author {get; set;}
        public DateTime Date {get; set;}
        public string Text {get; set;}
        public SavedAcordao Acordao {get; set;}
    }
}