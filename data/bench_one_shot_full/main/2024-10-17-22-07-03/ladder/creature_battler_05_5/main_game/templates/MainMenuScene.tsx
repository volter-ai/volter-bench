import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react'
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

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
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const buttonConfig = {
    play: { icon: <Play className="mr-2 h-4 w-4" />, label: "Play" },
    quit: { icon: <X className="mr-2 h-4 w-4" />, label: "Quit" },
  };

  return (
    <div className="w-full h-screen flex items-center justify-center bg-gradient-to-b from-purple-600 to-blue-800">
      <Card className="w-full max-w-[177.78vh] h-full max-h-[56.25vw] flex flex-col items-center justify-between p-8">
        <h1 className="text-6xl font-bold text-primary mb-8">Creature Battle</h1>
        
        <div className="flex flex-col space-y-4">
          {Object.entries(buttonConfig).map(([slug, config]) => (
            availableButtonSlugs.includes(slug) && (
              <Button
                key={slug}
                onClick={() => emitButtonClick(slug)}
                className="w-full"
                uid={`main-menu-${slug}-button`}
              >
                {config.icon}
                {config.label}
              </Button>
            )
          ))}
        </div>
      </Card>
    </div>
  );
}
