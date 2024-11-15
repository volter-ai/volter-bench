import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  imageUrl: string
  currentHp: number
  maxHp: number
}

interface CreatureCardSubComponentProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

let CreatureCardHeader = React.forwardRef<HTMLDivElement, CreatureCardSubComponentProps>(
  ({ uid, ...props }, ref) => <CardHeader ref={ref} {...props} />
)

let CreatureCardContent = React.forwardRef<HTMLDivElement, CreatureCardSubComponentProps>(
  ({ uid, ...props }, ref) => <CardContent ref={ref} {...props} />
)

let CreatureCardFooter = React.forwardRef<HTMLDivElement, CreatureCardSubComponentProps>(
  ({ uid, ...props }, ref) => <CardFooter ref={ref} {...props} />
)

let CreatureCardTitle = React.forwardRef<HTMLParagraphElement, CreatureCardSubComponentProps & React.HTMLAttributes<HTMLHeadingElement>>(
  ({ uid, ...props }, ref) => <CardTitle ref={ref} {...props} />
)

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, imageUrl, currentHp, maxHp, ...props }, ref) => {
    return (
      <Card ref={ref} className={cn("w-[350px]", className)} uid={uid} {...props}>
        <CreatureCardHeader uid={`${uid}-header`}>
          <CreatureCardTitle uid={`${uid}-title`}>{name}</CreatureCardTitle>
        </CreatureCardHeader>
        <CreatureCardContent uid={`${uid}-content`}>
          <img
            src={imageUrl}
            alt={name}
            className="w-full h-48 object-contain"
          />
        </CreatureCardContent>
        <CreatureCardFooter uid={`${uid}-footer`} className="flex flex-col gap-2">
          <div className="w-full flex justify-between text-sm">
            <span>HP</span>
            <span>{`${currentHp}/${maxHp}`}</span>
          </div>
          <Progress
            value={(currentHp / maxHp) * 100}
            className="w-full"
            uid={`${uid}-progress`}
          />
        </CreatureCardFooter>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"
CreatureCardHeader.displayName = "CreatureCardHeader"
CreatureCardContent.displayName = "CreatureCardContent"
CreatureCardFooter.displayName = "CreatureCardFooter"
CreatureCardTitle.displayName = "CreatureCardTitle"

CreatureCard = withClickable(CreatureCard)
CreatureCardHeader = withClickable(CreatureCardHeader)
CreatureCardContent = withClickable(CreatureCardContent)
CreatureCardFooter = withClickable(CreatureCardFooter)
CreatureCardTitle = withClickable(CreatureCardTitle)

export { 
  CreatureCard,
  CreatureCardHeader,
  CreatureCardContent,
  CreatureCardFooter,
  CreatureCardTitle
}
