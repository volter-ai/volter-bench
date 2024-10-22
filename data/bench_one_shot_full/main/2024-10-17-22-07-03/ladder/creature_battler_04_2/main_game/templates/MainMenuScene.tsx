import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Button } from "@/components/ui/button";
import { Play, X } from 'lucide-react'

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
  stats: Record<string, any>;
  meta: Record<string, any>;
  collections: Record<string, any>;
  uid: string;
  display_name: string;
  description: string;
}

export function MainMenuSceneView({ data }: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const { enabledUIDs } = useThingInteraction();

  const handleButtonClick = (slug: string) => {
    emitButtonClick(slug);
  };

  return (
    <div className="w-full h-full flex flex-col bg-gradient-to-b from-blue-900 to-blue-700">
      <div className="flex-1 flex items-center justify-center">
        <h1 className="text-4xl font-bold text-white">
          {data.display_name || "Game Title"}
        </h1>
      </div>
      <div className="mb-16 flex flex-col items-center space-y-4">
        {availableButtonSlugs.includes("play") && (
          <Button
            onClick={() => handleButtonClick("play")}
            className="w-48 text-lg"
            disabled={!enabledUIDs.includes("play")}
          >
            <Play className="mr-2 h-4 w-4" /> Play
          </Button>
        )}
        {availableButtonSlugs.includes("quit") && (
          <Button
            onClick={() => handleButtonClick("quit")}
            className="w-48 text-lg"
            disabled={!enabledUIDs.includes("quit")}
          >
            <X className="mr-2 h-4 w-4" /> Quit
          </Button>
        )}
      </div>
    </div>
  );
}
