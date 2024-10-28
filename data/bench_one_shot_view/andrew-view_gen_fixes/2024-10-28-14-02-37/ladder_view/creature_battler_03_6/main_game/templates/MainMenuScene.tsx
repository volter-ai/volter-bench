// Do not change these imports:
import { useCurrentButtons } from "@/lib/useChoices.ts";

// Import shadcn components
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

// You can change this import:
import { Play, X } from 'lucide-react'

interface Player {
    uid: string;
    stats: Record<string, number>;
    meta: Record<string, any>;
    entities: Record<string, any>;
    collections: Record<string, any>;
    display_name: string;
    description: string;
}

// the GameUIData interface should only be altered, not removed or renamed
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

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    const buttonConfig = {
        play: { text: 'Play', icon: Play },
        quit: { text: 'Quit', icon: X },
    };

    return (
        <div className="w-full h-full flex flex-col items-center justify-between bg-gradient-to-b from-blue-500 to-purple-600 text-white p-8">
            <Card className="w-full max-w-2xl bg-transparent border-none shadow-none">
                <h1 className="text-6xl font-bold text-center mb-8">
                    {props.data?.display_name || 'Game Title'}
                </h1>
            </Card>

            <Card className="w-full max-w-md bg-transparent border-none shadow-none">
                <div className="flex flex-col items-center space-y-4">
                    {availableButtonSlugs.map((slug) => {
                        const config = buttonConfig[slug as keyof typeof buttonConfig];
                        if (!config) return null;

                        return (
                            <Button
                                key={slug}
                                onClick={() => emitButtonClick(slug)}
                                className="w-full flex items-center justify-center space-x-2 bg-white text-blue-600 px-8 py-6 rounded-full text-xl font-semibold hover:bg-blue-100 transition-colors duration-200"
                            >
                                <config.icon className="w-6 h-6" />
                                <span>{config.text}</span>
                            </Button>
                        );
                    })}
                </div>
            </Card>
        </div>
    );
}
