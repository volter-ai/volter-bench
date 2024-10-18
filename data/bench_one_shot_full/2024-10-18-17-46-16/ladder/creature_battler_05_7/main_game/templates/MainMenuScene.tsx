import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';
import { Button } from "@/components/ui/button";

interface Player {
  uid: string;
  display_name?: string;
}

interface GameUIData {
  entities: {
    player?: Player;
  };
  uid: string;
}

export function MainMenuSceneView({ data }: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerName = data.entities.player?.display_name ?? "Player";

  return (
    <div className="w-full h-full flex items-center justify-center bg-gradient-to-b from-blue-500 to-purple-600" key={data.uid}>
      <div className="aspect-w-16 aspect-h-9 w-full max-w-4xl">
        <div className="flex flex-col justify-between items-center p-8 h-full">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold text-white mb-4">Creature Battle</h1>
            <p className="text-xl text-white">Welcome, {playerName}!</p>
          </div>
          
          <div className="space-y-4">
            {availableButtonSlugs.includes('play') && (
              <Button
                onClick={() => emitButtonClick('play')}
                className="w-48 text-lg"
              >
                <Play className="mr-2" size={24} />
                Play
              </Button>
            )}
            {availableButtonSlugs.includes('quit') && (
              <Button
                onClick={() => emitButtonClick('quit')}
                variant="destructive"
                className="w-48 text-lg"
              >
                <X className="mr-2" size={24} />
                Quit
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
