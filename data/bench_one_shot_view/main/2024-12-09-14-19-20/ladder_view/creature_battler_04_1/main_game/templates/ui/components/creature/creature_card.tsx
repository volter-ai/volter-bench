import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/custom/card"
import { Progress } from "@/components/ui/custom/progress"

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  image: string
  currentHp: number
  maxHp: number
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, image, currentHp, maxHp, ...props }, ref) => {
    return (
      <Card uid={uid} ref={ref} className={cn("w-[350px]", className)} {...props}>
        <CardHeader uid={`${uid}-header`}>
          <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
        </CardHeader>
        <CardContent uid={`${uid}-content`}>
          <img
            src={image}
            alt={name}
            className="w-full h-[200px] object-contain"
          />
        </CardContent>
        <CardFooter uid={`${uid}-footer`} className="flex flex-col gap-2">
          <div className="w-full flex justify-between">
            <span>HP</span>
            <span>{`${currentHp}/${maxHp}`}</span>
          </div>
          <Progress
            uid={`${uid}-progress`}
            value={(currentHp / maxHp) * 100}
            className="w-full"
          />
        </CardFooter>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
