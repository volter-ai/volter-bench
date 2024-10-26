import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

interface ExamplePlayer {
    uid: string,
    stats: {
        stat1: number,
    },
}

interface GameUIData {
    entities: {
        player: ExamplePlayer
    }
    stats: Record<string, any>;
    meta: Record<string, any>;
    collections: Record<string, any>;
    uid: string;
    display_name: string;
    description: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    const gameTitle = props.data?.display_name || "MainMenuScene";

    const buttonConfig = {
        play: { label: "Play", icon: Play },
        quit: { label: "Quit", icon: X },
    };

    return (
        <Card className="w-full h-full flex flex-col justify-between bg-gradient-to-b from-blue-500 to-purple-600 text-white">
            <div className="flex items-center justify-center mt-16">
                <h1 className="text-4xl md:text-6xl font-bold">{gameTitle}</h1>
            </div>
            
            <div className="flex flex-col items-center space-y-4 mb-16">
                {availableButtonSlugs.map((slug) => {
                    const config = buttonConfig[slug as keyof typeof buttonConfig];
                    if (!config) return null;

                    return (
                        <Button
                            key={slug}
                            onClick={() => emitButtonClick(slug)}
                            className="flex items-center justify-center space-x-2 bg-white text-blue-600 px-6 py-3 rounded-full font-semibold text-lg hover:bg-blue-100 transition-colors duration-200"
                        >
                            <config.icon className="w-6 h-6" />
                            <span>{config.label}</span>
                        </Button>
                    );
                })}
            </div>
        </Card>
    );
}
