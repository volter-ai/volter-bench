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
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    return (
        <div className="relative w-full h-full" style={{ aspectRatio: '16/9' }}>
            <Card className="w-full h-full bg-slate-900 flex flex-col items-center justify-between p-8">
                {/* Title Section */}
                <div className="w-full flex-1 flex items-center justify-center">
                    <h1 className="text-6xl font-bold text-white tracking-wider">
                        CREATURE BATTLE
                    </h1>
                </div>

                {/* Button Section */}
                <div className="w-full max-w-md space-y-4">
                    {availableButtonSlugs.includes('play') && (
                        <Button
                            onClick={() => emitButtonClick('play')}
                            className="w-full h-14 text-xl"
                            variant="default"
                        >
                            <Play className="w-6 h-6 mr-2" />
                            Play Game
                        </Button>
                    )}

                    {availableButtonSlugs.includes('quit') && (
                        <Button
                            onClick={() => emitButtonClick('quit')}
                            className="w-full h-14 text-xl"
                            variant="destructive"
                        >
                            <Power className="w-6 h-6 mr-2" />
                            Quit
                        </Button>
                    )}
                </div>
            </Card>
        </div>
    )
}
