import {useCurrentButtons} from "@/lib/useChoices.ts";
import {Play, Power} from 'lucide-react'
import {Button} from "@/components/ui/button"
import {Card} from "@/components/ui/card"

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
    display_name: string;
    uid: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    if (!props.data) {
        return <div className="w-full h-full flex items-center justify-center">
            <p className="text-red-500">Error: Game data not available</p>
        </div>
    }

    return (
        <Card className="relative w-full h-full bg-gradient-to-b from-blue-900 to-blue-950 flex flex-col items-center justify-between p-8 border-0">
            {/* Title Section */}
            <div className="w-full flex-1 flex items-center justify-center">
                <h1 className="text-6xl font-bold text-white tracking-wider">
                    {props.data.display_name || "Main Menu"}
                </h1>
            </div>

            {/* Button Section */}
            <Card className="w-full max-w-md space-y-4 bg-transparent border-0 shadow-none">
                {availableButtonSlugs.includes('play') && (
                    <Button
                        onClick={() => emitButtonClick('play')}
                        className="w-full h-16 text-xl bg-green-600 hover:bg-green-700"
                    >
                        <Play className="w-6 h-6 mr-2" />
                        Play Game
                    </Button>
                )}

                {availableButtonSlugs.includes('quit') && (
                    <Button
                        onClick={() => emitButtonClick('quit')}
                        variant="destructive"
                        className="w-full h-16 text-xl"
                    >
                        <Power className="w-6 h-6 mr-2" />
                        Quit
                    </Button>
                )}
            </Card>
        </Card>
    )
}
