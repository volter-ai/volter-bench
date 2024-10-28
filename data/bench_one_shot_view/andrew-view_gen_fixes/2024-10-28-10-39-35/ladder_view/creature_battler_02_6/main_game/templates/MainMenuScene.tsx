import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react'
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

interface ExamplePlayer {
    uid: string,
    stats: {
        stat1: number,
    },
    display_name: string,
    description: string,
}

interface GameUIData {
    entities: {
        player: ExamplePlayer
    }
    stats: Record<string, number>,
    meta: Record<string, any>,
    uid: string,
    display_name: string,
    description: string,
}

export function MainMenuSceneView({ data, uid }: { data: GameUIData, uid: string }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    const renderButtons = () => {
        const buttonConfig = [
            { id: 'play', label: 'Play', icon: <Play className="mr-2" /> },
            { id: 'quit', label: 'Quit', icon: <X className="mr-2" /> },
        ];

        return buttonConfig.map(button => (
            availableButtonSlugs.includes(button.id) && (
                <Button
                    key={button.id}
                    onClick={() => emitButtonClick(button.id)}
                    className="flex items-center justify-center"
                >
                    {button.icon}
                    {button.label}
                </Button>
            )
        ));
    };

    return (
        <Card className="w-full h-0 pb-[56.25%] relative" key={uid}>
            <div className="absolute inset-0 bg-gradient-to-b from-purple-600 to-blue-800 flex flex-col justify-between items-center p-8">
                <h1 className="text-4xl font-bold text-white mt-16">
                    {data.display_name || "Game Title"}
                </h1>
                <div className="flex flex-col space-y-4 mb-16">
                    {renderButtons()}
                </div>
            </div>
        </Card>
    );
}
