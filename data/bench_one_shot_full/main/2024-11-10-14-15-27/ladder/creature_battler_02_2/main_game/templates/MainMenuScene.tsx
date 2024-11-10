import {useCurrentButtons} from "@/lib/useChoices.ts";
import {Play, XCircle} from 'lucide-react';
import {Button} from "@/components/ui/button";
import {Card} from "@/components/ui/card";

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
        <Card className="w-full h-full flex flex-col items-center justify-between p-8 bg-gradient-to-b from-slate-900 to-slate-800">
            <div className="flex-1 flex items-center justify-center">
                <div className="w-96 h-32 bg-slate-700 flex items-center justify-center rounded-lg">
                    {/* Placeholder for title image - in real implementation this would use next/image or similar */}
                    <span className="text-slate-400">Title Image Placeholder</span>
                </div>
            </div>

            <div className="flex flex-col gap-4 mb-16">
                {availableButtonSlugs.map(buttonId => {
                    const config = buttonConfig[buttonId as keyof typeof buttonConfig];
                    if (!config) return null;

                    return (
                        <Button
                            key={buttonId}
                            onClick={() => emitButtonClick(buttonId)}
                            className="flex items-center justify-center px-8 py-6 min-w-[200px]"
                            variant="secondary"
                        >
                            {config.icon}
                            <span>{config.label}</span>
                        </Button>
                    );
                })}
            </div>
        </Card>
    );
}
