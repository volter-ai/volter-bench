import {useCurrentButtons} from "@/lib/useChoices.ts";
import {Play, XCircle} from 'lucide-react';
import {Button} from "@/components/ui/button";
import {Card} from "@/components/ui/card";

interface GameStats {
  [key: string]: number;
}

interface GameMeta {
  prototype_id: string;
  category: string;
}

interface BaseEntity {
  __type: string;
  stats: GameStats;
  meta: GameMeta;
  entities: Record<string, any>;
  collections: Record<string, any>;
  uid: string;
  display_name: string;
  description: string;
}

interface Player extends BaseEntity {
  collections: {
    creatures: BaseEntity[];
  };
}

interface GameUIData {
  entities: {
    player: Player;
  };
  uid: string;
  display_name: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    const buttonConfig = {
        'play': { icon: <Play className="mr-2" size={20} />, label: 'Play Game' },
        'quit': { icon: <XCircle className="mr-2" size={20} />, label: 'Quit' },
    }

    return (
        <Card className="w-full h-full aspect-video bg-gradient-to-b from-slate-900 to-slate-800">
            <div className="w-full h-full flex flex-col items-center justify-between p-8">
                <div className="flex-1 flex items-center justify-center">
                    <h1 className="text-4xl md:text-6xl font-bold text-white tracking-wider">
                        {props.data?.display_name || "GAME TITLE"}
                    </h1>
                </div>

                <div className="flex flex-col gap-4 mb-8">
                    {(availableButtonSlugs || []).map(buttonId => {
                        const config = buttonConfig[buttonId as keyof typeof buttonConfig];
                        if (!config) return null;

                        return (
                            <Button
                                key={buttonId}
                                onClick={() => emitButtonClick(buttonId)}
                                className="flex items-center justify-center px-8 py-6 min-w-[240px]"
                                variant="secondary"
                                size="lg"
                            >
                                {config.icon}
                                <span>{config.label}</span>
                            </Button>
                        );
                    })}
                </div>
            </div>
        </Card>
    );
}
