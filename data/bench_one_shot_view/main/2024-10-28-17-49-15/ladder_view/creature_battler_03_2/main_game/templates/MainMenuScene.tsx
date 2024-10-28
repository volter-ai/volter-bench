import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react'
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
  } = useCurrentButtons()

  const buttonConfig = {
    play: { text: 'Play', icon: Play },
    quit: { text: 'Quit', icon: X },
  }

  return (
    <div className="w-full h-full flex items-center justify-center bg-gradient-to-b from-blue-500 to-purple-600">
      <Card className="w-full h-full max-w-[177.78vh] max-h-[56.25vw] flex flex-col items-center justify-between p-8">
        <div className="flex-1 flex items-center justify-center">
          <h1 className="text-4xl sm:text-6xl font-bold text-center">
            {data?.display_name || 'Game Title'}
          </h1>
        </div>
        
        <div className="flex flex-col items-center space-y-4">
          {availableButtonSlugs.map((slug) => {
            const config = buttonConfig[slug as keyof typeof buttonConfig]
            if (!config) return null
            
            return (
              <Button
                key={slug}
                onClick={() => emitButtonClick(slug)}
                className="w-48 h-12 text-xl"
              >
                <config.icon className="w-6 h-6 mr-2" />
                {config.text}
              </Button>
            )
          })}
        </div>
      </Card>
    </div>
  )
}
