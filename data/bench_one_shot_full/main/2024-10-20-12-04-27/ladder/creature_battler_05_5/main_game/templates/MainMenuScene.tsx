import { useCurrentButtons } from "@/lib/useChoices.ts";
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

  const buttonConfig = {
    play: { text: "Play", icon: Play },
    quit: { text: "Quit", icon: X },
  };

  return (
    <div className="w-full h-full flex items-center justify-center bg-gradient-to-b from-blue-500 to-purple-600">
      <div className="w-full max-w-[177.78vh] h-full max-h-[56.25vw] flex flex-col items-center justify-between p-8">
        <div className="w-full flex-1 flex items-center justify-center">
          <h1 className="text-6xl font-bold text-white text-center">
            Game Title
          </h1>
        </div>

        <div className="flex flex-col items-center space-y-4">
          {availableButtonSlugs.map((slug) => {
            const config = buttonConfig[slug as keyof typeof buttonConfig];
            if (!config) return null;

            return (
              <Button
                key={slug}
                onClick={() => emitButtonClick(slug)}
                className="w-48 h-12 text-lg"
              >
                <config.icon className="mr-2 h-5 w-5" />
                {config.text}
              </Button>
            );
          })}
        </div>

        <div className="text-white text-sm mt-4">
          {data.entities.player?.display_name ?? "Unknown Player"}
        </div>
      </div>
    </div>
  );
}
