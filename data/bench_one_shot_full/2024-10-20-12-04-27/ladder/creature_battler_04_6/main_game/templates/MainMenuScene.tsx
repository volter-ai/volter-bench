import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Button } from "@/components/ui/button";
import { Play, X } from 'lucide-react';

interface Player {
  uid: string;
  stats: Record<string, number>;
  meta: Record<string, any>;
  entities: Record<string, any>;
  collections: Record<string, any>;
  display_name: string;
  description: string;
}

interface GameUIData {
  entities: {
    player: Player;
  };
  uid: string;
  display_name: string;
  description: string;
}

export function MainMenuSceneView({ data, uid }: { data: GameUIData; uid: string }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const getButtonIcon = (slug: string) => {
    switch (slug) {
      case 'play':
        return <Play className="mr-2 h-4 w-4" />;
      case 'quit':
        return <X className="mr-2 h-4 w-4" />;
      default:
        return null;
    }
  };

  const getButtonText = (slug: string) => {
    return slug.charAt(0).toUpperCase() + slug.slice(1);
  };

  return (
    <div className="w-full h-full flex flex-col justify-between items-center p-8 bg-gray-800 text-white">
      <div className="text-4xl font-bold mt-16">
        {data.display_name || "Game Title"}
      </div>
      
      <div className="flex flex-col items-center space-y-4 mb-16">
        {availableButtonSlugs.map((slug) => (
          <Button
            key={slug}
            onClick={() => emitButtonClick(slug)}
            className="w-48"
          >
            {getButtonIcon(slug)}
            {getButtonText(slug)}
          </Button>
        ))}
      </div>
    </div>
  );
}
