using System;
using Dossier.Core.Entities;

namespace Dossier.Api.Models 
{
    public class CommentDto 
    {
        public int Id {get;set;}
        public string Author {get; set;}
        public DateTime Date {get; set;}
        public string Text {get; set;}

        public static CommentDto FromEntity(Comment c) => new CommentDto()
        {
            Id = c.Id,
            Author = c.Author,
            Date = c.Date,
            Text = c.Text
        };
    }
}