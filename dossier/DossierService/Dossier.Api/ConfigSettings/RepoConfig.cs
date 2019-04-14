using Dossier.Infrastructure.ConfigSettings;

namespace Dossier.Api.ConfigSettings {
    public class RepoConfig : IRepoConfig
    {
        public string DossierConnString {get; set;}
    }
}