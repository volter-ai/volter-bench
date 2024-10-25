import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';
import { Button } from "@/components/ui/button";

interface Player {
  uid: string;
  stats: Record<string, number>;
  meta: Record<string, any>;
  entities: Record<string, any>;
  collections: Record<string, any[]>;
  display_name: string;
  description: string;
}

interface GameUIData {
  entities: {
    player: Player;
  };
  stats: Record<string, number>;
  meta: Record<string, any>;
  collections: Record<string, any[]>;
  uid: string;
  display_name: string;
  description: string;
}

export function MainMenuSceneView({ data, uid }: { data: GameUIData; uid: string }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const renderButtons = () => {
    return (
      <div className="flex flex-col space-y-4">
        {availableButtonSlugs.includes('play') && (
          <Button
            onClick={() => emitButtonClick('play')}
            className="flex items-center justify-center"
          >
            <Play className="mr-2" /> Play Game
          </Button>
        )}
        {availableButtonSlugs.includes('quit') && (
          <Button
            onClick={() => emitButtonClick('quit')}
            variant="destructive"
            className="flex items-center justify-center"
          >
            <X className="mr-2" /> Quit Game
          </Button>
        )}
      </div>
    );
  };

  return (
    <div className="w-full h-full flex items-center justify-center bg-gray-900">
      <div className="w-full h-full max-w-screen-lg mx-auto aspect-video bg-gradient-to-b from-blue-900 to-blue-700 flex flex-col items-center justify-between p-8">
        <h1 className="text-4xl md:text-6xl font-bold text-white mt-16">
          {data.display_name || "Game Title"}
        </h1>
        {data.entities.player && (
          <p className="text-white text-xl">
            Welcome, {data.entities.player.display_name}!
          </p>
        )}
        <div className="flex-grow" />
        {renderButtons()}
      </div>
    </div>
  );
}
