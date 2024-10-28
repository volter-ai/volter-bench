import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

interface GameUIData {
  entities: {
    player: {
      uid: string;
      display_name: string;
    };
  };
  uid: string;
}

export function MainMenuSceneView({ data }: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerName = data.entities.player?.display_name || "Player";

  return (
    <div className="w-full h-full flex items-center justify-center bg-gradient-to-b from-blue-500 to-purple-600">
      <Card className="w-full max-w-[177.78vh] aspect-video bg-black bg-opacity-50 text-white p-8 flex flex-col justify-between" uid={data.uid}>
        <div className="text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-4">Creature Battle Game</h1>
          <p className="text-xl">Welcome, {playerName}!</p>
        </div>
        
        <div className="flex flex-col items-center">
          {availableButtonSlugs.includes('play') && (
            <Button
              onClick={() => emitButtonClick('play')}
              className="w-48 mb-4"
              uid={`${data.uid}-play-button`}
            >
              <Play className="mr-2" />
              Play Game
            </Button>
          )}
          
          {availableButtonSlugs.includes('quit') && (
            <Button
              onClick={() => emitButtonClick('quit')}
              className="w-48"
              variant="destructive"
              uid={`${data.uid}-quit-button`}
            >
              <X className="mr-2" />
              Quit Game
            </Button>
          )}
        </div>
      </Card>
    </div>
  );
}
