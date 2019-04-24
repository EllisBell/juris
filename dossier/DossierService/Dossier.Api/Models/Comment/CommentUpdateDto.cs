using System;
using System.ComponentModel.DataAnnotations;

namespace Dossier.Api.Models 
{
    public class CommentUpdateDto 
    {   
        [Required]
        public string Text {get; set;}
    }
}