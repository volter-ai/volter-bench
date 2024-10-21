import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

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
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const renderButtons = () => {
    return (
      <div className="flex flex-col space-y-4">
        {availableButtonSlugs.includes('play') && (
          <Button
            variant="default"
            onClick={() => emitButtonClick('play')}
            className="flex items-center justify-center px-6 py-3 text-lg font-semibold"
          >
            <Play className="mr-2" size={24} />
            Play
          </Button>
        )}
        {availableButtonSlugs.includes('quit') && (
          <Button
            variant="destructive"
            onClick={() => emitButtonClick('quit')}
            className="flex items-center justify-center px-6 py-3 text-lg font-semibold"
          >
            <X className="mr-2" size={24} />
            Quit
          </Button>
        )}
      </div>
    );
  };

  return (
    <Card className="w-full h-full bg-gradient-to-b from-blue-900 to-blue-700 flex flex-col items-center justify-between p-8" style={{ aspectRatio: '16/9' }}>
      <h1 className="text-5xl font-bold text-white mt-16">
        {data.display_name || "Game Title"}
      </h1>
      <div className="mb-16">
        {renderButtons()}
      </div>
    </Card>
  );
}
