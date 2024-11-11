import {useCurrentButtons} from "@/lib/useChoices.ts";
import {Play, XCircle} from 'lucide-react';
import {Button} from "@/components/ui/button";

interface GameStats {
    hp?: number;
    max_hp?: number;
    attack?: number;
    defense?: number;
    speed?: number;
    base_damage?: number;
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
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    const buttonConfig = {
        'play': {
            label: 'Play Game',
            icon: <Play className="mr-2 h-4 w-4" />,
        },
        'quit': {
            label: 'Quit Game',
            icon: <XCircle className="mr-2 h-4 w-4" />,
        }
    }

    return (
        <div className="w-full h-full flex flex-col items-center justify-between p-8 bg-gradient-to-b from-slate-900 to-slate-800">
            <div className="flex-1 flex items-center justify-center">
                <h1 className="text-4xl font-bold text-white tracking-wider">
                    Creature Battle Game
                </h1>
            </div>

            <div className="flex flex-col gap-4 mb-16">
                {availableButtonSlugs.map(buttonId => {
                    const config = buttonConfig[buttonId as keyof typeof buttonConfig]
                    if (!config) return null

                    return (
                        <Button
                            key={buttonId}
                            onClick={() => emitButtonClick(buttonId)}
                            className="min-w-[200px]"
                        >
                            {config.icon}
                            {config.label}
                        </Button>
                    )
                })}
            </div>
        </div>
    )
}
