import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

interface Player {
  uid: string;
  display_name?: string;
  description?: string;
}

interface GameUIData {
  entities: {
    player?: Player;
  };
  stats: Record<string, any>;
  meta: Record<string, any>;
  collections: Record<string, any>;
  uid: string;
  display_name?: string;
  description?: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerName = props.data.entities.player?.display_name ?? "Player";

  return (
    <div className="w-full h-full bg-gradient-to-b from-blue-500 to-blue-700 flex flex-col items-center justify-between p-8">
      <Card className="w-full h-1/3 flex items-center justify-center bg-opacity-20">
        <h1 className="text-4xl font-bold text-white text-center">
          {props.data.display_name ?? "Game Title"}
        </h1>
      </Card>

      <div className="text-xl text-white mb-8">
        Welcome, {playerName}!
      </div>

      <div className="flex flex-col space-y-4">
        {availableButtonSlugs.includes('play') && (
          <Button
            onClick={() => emitButtonClick('play')}
            className="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded flex items-center justify-center"
          >
            <Play className="mr-2" /> Play Game
          </Button>
        )}
        {availableButtonSlugs.includes('quit') && (
          <Button
            onClick={() => emitButtonClick('quit')}
            className="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded flex items-center justify-center"
          >
            <X className="mr-2" /> Quit Game
          </Button>
        )}
      </div>
    </div>
  );
}
