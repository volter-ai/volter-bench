import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';
import { Button } from "@/components/ui/button";

interface GameUIData {
  entities: {
    player: {
      uid: string;
      stats: Record<string, number>;
      meta: Record<string, any>;
      entities: Record<string, any>;
      collections: Record<string, any>;
      display_name: string;
      description: string;
    };
  };
}

export function MainMenuSceneView({ data }: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const {
    enabledUIDs
  } = useThingInteraction();

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

  return (
    <div className="w-full h-full flex flex-col items-center justify-between bg-gradient-to-b from-blue-500 to-purple-600 p-8">
      <div className="w-full h-1/3 flex items-center justify-center">
        <div className="bg-white bg-opacity-20 rounded-lg p-8 text-4xl font-bold text-white">
          Game Title
        </div>
      </div>

      <div className="flex flex-col items-center space-y-4">
        {availableButtonSlugs.map((slug) => (
          <Button
            key={slug}
            uid={slug}
            onClick={() => emitButtonClick(slug)}
            className="w-48 h-12 text-lg capitalize"
            disabled={!enabledUIDs.includes(slug)}
          >
            {getButtonIcon(slug)}
            {slug}
          </Button>
        ))}
      </div>

      <div className="text-white text-sm mt-4">
        {data.entities.player && (
          <>
            <p>Welcome, {data.entities.player.display_name}!</p>
            <p>Creatures: {data.entities.player.collections.creatures?.length || 0}</p>
          </>
        )}
      </div>
    </div>
  );
}
